1.1:
-pbkdf2 is a key derivation function using the input passphrase (with salt) and hashes it many times to create a key.  Encrypting with a passphrase requires pbkdf2 to turn that passphrase into a usable key that is secure.

1.2: 
The checksums for the files are different because the encryption process begins with a pseudo-random block via the initialization vector, which encrypts identical messages differently.  An encryption scheme that produces two identical encrypted files (1:1 input:output) could be more predictable and even derivable, making the encrypted files more vulnerable.

1.3: 
ECB produces 2 distinct blocks with its most common block repeating 12 times, while CBC produced 13 unique blocks.  ECB revealed that there are patterns within the input, which is useful to an attacker who can have an easier time guessing the content.  Given this, if I were told that a system encrypts database records with AES, I would ask specifically what operation/mode was used to encrypt the files to make sure that it is something that does not preserve any discernible pattern or information about the input.

2: 
The SHA-256 hash doesn't protect my colleague because when used by itself, it can only indicate whether something has changed and does not prevent attacks from happening.  When HMAC is used, only the signature used by the sender can be accepted, with modifications invalidating that signature, providing authentication.  With SHA-256 only, an attacker can change the file and hash before sending using the public key, making it hard to determine who wrote the message.  When HMAC is used with SHA-256, the attacker can now see the message, but any modifications to the file will invalidate its signature, failing authentication blatantly.

3: 
That the keyserver would not publish your email address until a verification link is clicked on proves that the user who sent the key(s) also has (in)direct access to the same email address, but it does not prove that it is the same user and certainly does not prove if it is the correct/authorized user.  To see if a downloaded public key really belongs to my classmate, my first thought would be to ask them in person (or over a different network,such as phone call) to see if that information is available, which would avoid the attacker-controlled network altogether.

4.2: 
In the pubkey enc packet is the session key encrypted using the public key generated earlier with RSA, and the encrypted data packet contains the encrypted message (encrypted with the session key above it).  GPG uses this approach instead of encrypting the entire message with RSA because RSA is unwieldy for bulk data, and if the private RSA key is compromised, then all subsequent messages in the same session are compromised.  The choice to use RSA for encrypting the key and then a faster function for the message is known as hybrid encryption.

4.3: 
The sender's private key is used for signing, the sender's public key is used for verifying, the recipient's public key is used for encryption, and the recipient's private key is used for decryption.  One security property provided by signing is authentication - proving that only the original sender could have sent that message, as only the sender can produce valid signatures.

5: 
The much smaller Ed25519 key is not necessarily weaker than RSA-4096 because it uses a different difficult problem that is also unfeasible to undo to find the starting point.  A 256-bit key is about as strong as a 3072-bit RSA key.

7.1:
Prompt: "Write me a Python function that encrypts a file with AES"
Model: Claude Sonnet 5.5 Medium
 
7.2:
-Without specification, to test, the model's generated code hard-codes the password and the parameters into the script.
-File decryption is included in the same file automatically.
-Plaintext file is not deleted after encryption.

7.3:
I removed the decryption function from being in the same file as encryption to keep the script performing only its intended purpose.  This limits the damages if the file gets compromised and prevents an attacker from using the same script  to decrypt other encrypted files on the system.
I removed the hard-coded password and parameters and instead made them environmental variables, which prevents vital info (pw) to be compromised if the script were to be compromised.
I added a line to delete the original plaintext secret.txt file to remove the unencrypted message completely, which prevents it from being viewed plainly entirely unless decrypted.
